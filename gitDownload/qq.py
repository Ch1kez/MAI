import requests

profName = 'Ch1kez'
RepName = 'MAI'


def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

filename = download_file(f'https://github.com/{profName}/{RepName}/archive/refs/heads/main.zip')
print(filename)