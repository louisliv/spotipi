from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="spotipi",
    version="0.1.4",
    description="A Spotify playback control system using RFID cards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Louis Livingston",
    author_email="livingston.louis@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        "console_scripts": [
            "spotipi-server=server:app",
            "spotipi-reader=reader:main",
            "spotipi-fake-mfrc=spotipi.fake_mfrc:send_fake_rfid",
            "spotipi-notifications=notifications_service:main",
            "spotipi-player=player_service:main",
            "spotipi-scanner=scanner_service:main",
        ],
    },
)
