workflow "Deploy to Docker Hub" {
  on = "push"
  resolves = ["Push to Docker Hub"]
}

action "Login to Docker Hub" {
  uses = "actions/docker/login@86ff551d26008267bb89ac11198ba7f1d807b699"
  secrets = ["DOCKER_USERNAME", "DOCKER_PASSWORD"]
}

action "Build Docker Image" {
  uses = "actions/docker/cli@86ff551d26008267bb89ac11198ba7f1d807b699"
  args = "build -t nikoheikkila/utility-belt:latest -t nikoheikkila/utility-belt:$GITHUB_REF ."
  needs = ["Login to Docker Hub"]
}

action "Push to Docker Hub" {
  uses = "actions/docker/cli@86ff551d26008267bb89ac11198ba7f1d807b699"
  needs = ["Build Docker Image"]
  args = "push nikoheikkila/utility-belt"
}
