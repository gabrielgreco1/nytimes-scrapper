from search import NYTSearch

if __name__ == "__main__":
    nyt_search = NYTSearch("health")
    results = nyt_search.run()
    for result in results:
        print(result)
    # nyt_search.driver.quit()