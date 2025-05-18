current="$SHELL"

if [ "$current" = "/bin/zsh" ]; then
  echo "alias mini=\"~/mini/python/main.py\"" >> ~/.zshrc
elif [ "$current" = "/bin/bash" ]; then
  echo "alias mini=\"~/mini/python/main.py\"" >> ~/.bashrc
fi