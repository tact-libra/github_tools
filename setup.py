import setuptools

with open("requirements.txt") as f:
  req = f.read().splitlines()

setuptools.setup(
  name="gh_tools",
  version="0.1",
  author="kurages",
  author_email="kurages.git@outlook.jp",
  description="",
  url="https://github.com/kurages/github_tools",
  packages=setuptools.find_packages(),
  install_requires=req,
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  entry_points = {
    'console_scripts': ['gh_tools = src.gh_tools:main']
  },
  python_requires='>=3.6'
)