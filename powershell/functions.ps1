function ConvertImageToBase64 {
    param(
        [string]$imagePath
    )

    $image = [System.IO.File]::ReadAllBytes($imagePath)
    $base64 = [System.Convert]::ToBase64String($image)

    return $base64
}

function ConvertBase64ToImage {
    param(
        [string]$base64,
        [string]$outputPath
    )

    $image = [System.Convert]::FromBase64String($base64)
    [System.IO.File]::WriteAllBytes($outputPath, $image)
}

