$env:tag = "fn_image_manipulation:v2"

$env:container_id = docker ps -q -f "ancestor=$env:tag"

# Display the Docker container ID
Write-Output "Container ID: $env:container_id"

Write-Output "Stopping container $env:container_id"

docker stop $env:container_id

Write-Output "Removing container $env:container_id"

docker rm $env:container_id

# remove local image
Write-Output "Removing local image $env:tag"

docker rmi $env:tag
