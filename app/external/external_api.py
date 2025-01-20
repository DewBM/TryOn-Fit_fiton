import httpx
from gradio_client import Client, handle_file
from pathlib import Path


class ExternalAPIClient:
    BASE_URL = "https://external.api.example.com"

    @staticmethod
    async def generateFitOn(user_image: Path, garment_url: str):
        """
        Sends a GET request to the external API.

        :param endpoint: The specific API endpoint to hit (relative to BASE_URL).
        :param params: Query parameters for the GET request.
        :return: The response data in JSON format.
        """

        client = Client("levihsu/OOTDiffusion")

        result = client.predict(
            vton_img=handle_file(user_image),
            garm_img=handle_file(garment_url),
            n_samples=1,
            n_steps=40,
            image_scale=3,
            seed=-1,
            api_name="/process_hd"
        )

        print("FitOn Result: ", result)
        return result

        # url = f"{ExternalAPIClient.BASE_URL}/{endpoint}"
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(url, params=params)
        #     response.raise_for_status()  # Raise exception for HTTP errors
        #     return response.json()
