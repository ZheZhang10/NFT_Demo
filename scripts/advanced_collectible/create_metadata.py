import json
from os import path
from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import os

breed_to_img = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}


def main():
    # get the latest contract
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectible = advanced_collectible.tokenCounter()
    print(f"There are {number_of_collectible} collectibles")
    # get the corresponding breed name
    for tokenId in range(number_of_collectible):
        breed = get_breed(advanced_collectible.tokenIdToBreed(tokenId))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{tokenId}-{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite.")
        else:
            print("Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            # get the image URI from ipfs
            image_rui = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_rui = upload_to_ipfs(image_path)
            image_rui = image_rui if image_rui else breed_to_img[breed]

            collectible_metadata["image"] = image_rui
            # dump collectible_metadata dictionary as json file output as meta_file_name name
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)




# https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json
def upload_to_ipfs(filepath):
    # read the image as binary
    with Path(filepath).open("rb") as fp:
        binary_image = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        end_point = "/api/v0/add"
        # post img
        response = requests.post(ipfs_url + end_point, files={"file": binary_image})
        ipfs_hash = response.json()["Hash"]
        # "./img/0-PUG.png" -> "0-PUG.png"
        file_name = filepath.split("/")[-1:][0]
        img_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={file_name}"
        print(img_uri)
        return img_uri

