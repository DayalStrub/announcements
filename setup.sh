# TODO set up .devcontainer for Codespaces

# install aws cli - see https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# install quarto-cli see https://quarto.org/docs/download/tarball.html
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.5.56/quarto-1.5.56-linux-amd64.tar.gz
mkdir ~/opt
tar -C ~/opt -xvzf quarto-1.5.56-linux-amd64.tar.gz
ln -s ~/opt/quarto-1.5.56/bin/quarto ~/.local/bin/quarto
