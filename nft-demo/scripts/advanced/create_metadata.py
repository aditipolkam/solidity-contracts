from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        # breed = advanced_collectible.tokenIdToBreed(token_id)
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_filename = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )

        collectible_metadata = metadata_template

        if Path(metadata_filename).exists():
            print(f"Metadata file {metadata_filename} already exists.")
        else:
            print(f"Creating metadata file {metadata_filename}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            print(collectible_metadata)
            image_filepath = "./img" + breed.lower().replace("_", "-") + ".png"
            image_uri = upload_to_ipfs(image_filepath)
            collectible_metadata["image"] = image_uri


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url+endpoint, files ="file": image_binary)
        ipfs_hash = response.json()["Hash"]
        # "./img/puppy.png" -> "puppy.png"
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri