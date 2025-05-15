# Filmception
This project focuses on movie genre classification/prediction based on the movie summary
It also translates the summary into different languages (currently in Urdu, Arabic, and Korean)


## How to use it
- Clone the repository `Filmception`
```bash
  clone https://github.com/mimikyu-101/Filmception.git
  cd Filmception
```
- Preferablly make python virtual environment
```bash
  python -m venv ai_project
  .\ai_project\Scripts\activate
```
- Run the `requirements.txt` file
```bash
    python.exe -m pip install -r requirements.txt
```
- Use the datasets and run the preprocessing scripts
- Start the model trainig on the final datasets
    * `train_genre_dataset.tsv`
    * `test_genre_dataset.tsv`
- Move the following files in the 'modules' directory
    * `lightgbm_genre_classifier.pkl`
    * `tfidf_vectorizer.pkl`
    * `genre_columns.json`
- Finally, execute the `tools.py` script

  
## Authors

- [@Abdullah Nadeem](https://github.com/mimikyu-101)

- [@Nameer Khan](https://github.com/nameerkhan7)
