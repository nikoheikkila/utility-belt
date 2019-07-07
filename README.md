# Utility Belt

This is a collection of utility scripts made mostly with Python and intended to be run from a Docker container to guarantee multi-platform compatibility.

## Scripts

- [**Link Check**](./scripts/link-check.py) - checks a given URL for outbound links and their status, good for detecting broken links on a web page

## Usage

Pull and run from the [<u>Docker Hub</u>][hub] like so (replace bracketed values with real ones):

```bash
docker pull nikoheikkila/utility-belt
docker run -it --name utility-belt nikoheikkila/utility-belt <script.py> [<arguments>]
```

## Cleaning Up

Specify the `--rm` flag when running container or remove it after using as usual:

```bash
docker rm -f utility-belt
```

## Contributing

All the utilities are located under the `scripts/` directory. Take a look and open a pull request if you have got suggestions.

After implementing your script and saving it into the correct location test it by building the Docker image locally. Image uses the official Alpine variant of Python and scripts are passed to the Python interpreter directly. Dependencies are defined in `Pipfile` and installed with `pipenv` during image build.

Once your contributions have been merged, _GitHub Actions_ pipeline will push a fresh image to Docker Hub automatically tagging it with `latest`.

[hub]: https://cloud.docker.com/u/nikoheikkila/repository/docker/nikoheikkila/utility-belt
