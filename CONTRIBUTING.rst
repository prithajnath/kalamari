## Contributing to Kalamari
Thank you so much for considering contributing to Kalamari

### First time setup
Since this package is not available via PyPI yet, you have to install it manually. You'll need to fork the repo first. After forking, clone your fork in your local machine and run the following command

```sh
python3 setup.py sdist
```
This will create a sub-directory called `dist` which will contain a compressed archive file. The file format defaults to `tar.gz` on POSIX systems and `.zip` on Windows.

After creating this archive file, you can install the package via `pip3`

```sh
sudo pip3 install kalamari-0.1dev.tar.gz
```

Now add the main repository as a remote to update later

```sh
git remote add kalamari https://github.com/prithajnath/kalamari
git fetch kalamari
```
Finally, install Kalamari in editable mode with development dependencies
```sh
pip3 install -e ".[dev]"
```
### Workflow

Make your changes and commit your code along the way. Before committing, it's a good idea to run the test suite to make sure you didn't break anything. So before staging your changes and committing the, just run the following command

```sh
pytest
```
If it passes all the tests, then you're looking good. Push your commits to GitHub and create a pull request.
