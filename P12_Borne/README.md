# BOE Data Scraper

## Overview

This project is a web scraper designed to extract information about companies created and deleted in Spain from the BOE (Boletín Oficial del Estado) website. The scraper gathers data such as company names, registration dates, and deletion information.

## Features

- **Web Scraping**: Utilizes web scraping techniques to extract relevant data from the BOE website.
- **Data Processing**: Processes the scraped data to extract key information about newly created and deleted companies.
- **Export**: Provides options to export the collected data to various formats (e.g., CSV, JSON) for further analysis.

## Prerequisites

Make sure you have the following installed:

- Python 3.x
- Required Python packages (install using `pip install -r requirements.txt`)

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/boe-data-scraper.git
    ```

2. Install dependencies:

    ```bash
    cd P12_Borne
    pip install -r requirements.txt
    ```

3. Run the scraper:

    ```bash
    python __main.py__
    ```

4. Check the exported data:

    The scraped data will be exported to the `output` folder in the specified format.

## Configuration

- Customize the scraper settings in the `config.py` file, such as the target URL and export format.

## Disclaimer

Use this scraper responsibly and in compliance with the terms of service of the BOE website. Respect the website's policies and legal requirements.

## Contributing

If you'd like to contribute to the project, feel free to submit a pull request or open an issue.

## License

This project is licensed under the [MIT License](LICENSE).

