import os
import urllib3


# Get GitHub Repo as Zip
def get_github_repo(
    owner: str, repo: str, ref: str, token: str, outfile: str = "repo.zip"
) -> str:
    """down the git repository as a zip

    Args:
        owner (str): owner of the repository
        repo (str): repository name
        ref (str): branch of the repository
        token (str): pat to be used for authentication
        outfile (str, optional): name of the file to be created when repository is downloaded. Defaults to 'repo.zip'.

    Returns:
        str: returns the name of the zip file
    """
    http = urllib3.PoolManager()

    print(f"Downloading GitHub repository {owner}/{repo} \n")

    # api url for downloading repository as zip file
    url = f"https://api.github.com/repos/{owner}/{repo}/zipball/{ref}"

    # api request to download zip file (github repo)
    r = http.request(
        "GET",
        url=url,
        preload_content=False,
        headers={"Authorization": "Bearer " + token},
    )

    with open(outfile, "wb") as out:
        while True:
            data = r.read(64)
            if not data:
                break
            out.write(data)
    r.release_conn()

    print(f"GitHub repository {owner}/{repo} is now available")

    return outfile


# main function
def main():
    owner = input("Enter repository owner name: ")
    print(f"Repository owner: {owner}")

    repo = input("Enter repository name: ")
    print(f"Repository owner: {repo}")

    ref = input("Enter repository branch name to download: ")
    print(f"Repository owner: {ref}")

    repo_visibility = input("Enter repository visibility (private/public): ")
    print(f"Repository visibility: {repo_visibility}")

    if repo_visibility == "private":  # github repository is private
        if not "GIT_PAT" in os.environ:  # GIT_PAT is not available
            print(f"GIT_PAT not found. Enter the GitHub PAT as an environment variable")
            exit
        else:  # GIT_PAT is available
            token = os.environ.get("GIT_PAT")
            get_github_repo(
                owner=owner, repo=repo, ref=ref, token=token
            )  # Get the Private GitHub Repository
    else:  # github repository is public
        get_github_repo(
            owner=owner, repo=repo, ref=ref
        )  # Get the Public GitHub Repository


if __name__ == "__main__":
    main()
