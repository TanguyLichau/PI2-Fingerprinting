# Web Fingerprinting Project

This school project was aiming to discover how web fingerprinting really works under the hood by deep diving into four key aspects:

- IP quality
- HTTP headers
- TLS layer
- JavaScript fingerprinting.

The goal for this script is to discern variations in site protection mechanisms by trying different types of requests.

## Execution

### Requirements

- Python 3.x
- Necessary Python packages (specified in requirements.txt)
- Environment variables for proxy URLs (WEAK_PROXY_URL, STRONG_PROXY_URL)

### Usage

1. Clone the repository

```bash
git clone https://github.com/your-username/your-web-fingerprinting-repo.git
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Run the script

```bash
python cffi.py --url "target_url"
```

or

```bash
python cffi.py --urls "url_list.txt"
```

### Results

| Website                                                                                                          | Basic Request      | Basic request + Weak Proxy | Basic request + Strong Proxy | CFFI               | CFFI + Weak Proxy  | CFFI + Strong Proxy |
| ---------------------------------------------------------------------------------------------------------------- | ------------------ | -------------------------- | ---------------------------- | ------------------ | ------------------ | ------------------- |
| [fnac.com](https://www.fnac.com/...)                                                                             | :o:                | :o:                        | :o:                          | :o:                | :o:                | :o:                 |
| [reddit.com](https://www.reddit.com)                                                                             | :o:                | :o:                        | :o:                          | :o:                | :o:                | :o:                 |
| [tiktok.com](https://www.tiktok.com)                                                                             | :o:                | :o:                        | :o:                          | :white_check_mark: | :white_check_mark: | :white_check_mark:  |
| [snipesusa.com](https://www.snipesusa.com)                                                                       | :o:                | :o:                        | :o:                          | :o:                | :o:                | :white_check_mark:  |
| [courir.com](https://www.courir.com)                                                                             | :white_check_mark: | :white_check_mark:         | :white_check_mark:           | :white_check_mark: | :white_check_mark: | :white_check_mark:  |
| [twitter.com](https://twitter.com/Haroon_HMM/status/:white_check_mark:746598:white_check_mark::o:5246736633)     | :o:                | :o:                        | :o:                          | :o:                | :o:                | :o:                 |
| [alibaba.com](https://www.alibaba.com/)                                                                          | :white_check_mark: | :white_check_mark:         | :white_check_mark:           | :white_check_mark: | :white_check_mark: | :white_check_mark:  |
| [vipkid.com](https://www.vipkid.com/zh-cn)                                                                       | :o:                | :o:                        | :o:                          | :o:                | :o:                | :o:                 |
| [chuangshi.qq.com](http://chuangshi.qq.com/)                                                                     | :white_check_mark: | :white_check_mark:         | :white_check_mark:           | :o:                | :o:                | :o:                 |
| [github.com/Sacha924](https://github.com/Sacha924)                                                               | :white_check_mark: | :white_check_mark:         | :white_check_mark:           | :white_check_mark: | :white_check_mark: | :white_check_mark:  |
| [yvelines.gouv.fr](https://www.yvelines.gouv.fr/)                                                                | :o:                | :o:                        | :o:                          | :white_check_mark: | :white_check_mark: | :white_check_mark:  |
| [binance.com/fr](https://www.binance.com/fr)                                                                     | :white_check_mark: | :white_check_mark:         | :white_check_mark:           | :white_check_mark: | :white_check_mark: | :o:                 |
| [esilv.fr](https://www.esilv.fr/)                                                                                | :white_check_mark: | :white_check_mark:         | :white_check_mark:           | :white_check_mark: | :white_check_mark: | :white_check_mark:  |
| [usembassy.gov/fr](https://fr.usembassy.gov/fr/)                                                                 | :white_check_mark: | :white_check_mark:         | :white_check_mark:           | :white_check_mark: | :white_check_mark: | :white_check_mark:  |
| [linkedin.com/in/emmanuelmacron](https://www.linkedin.com/in/emmanuelmacron/)                                    | :o:                | :o:                        | :o:                          | :white_check_mark: | :white_check_mark: | :white_check_mark:  |
| [dgse.gouv.fr](https://www.dgse.gouv.fr/fr)                                                                      | :o:                | :o:                        | :o:                          | :o:                | :white_check_mark: | :white_check_mark:  |
| [labanquepostale.fr](https://www.labanquepostale.fr/)                                                            | :white_check_mark: | :white_check_mark:         | :white_check_mark:           | :white_check_mark: | :white_check_mark: | :white_check_mark:  |
| [grayscale.com](https://www.grayscale.com/)                                                                      | :white_check_mark: | :white_check_mark:         | :o:                          | :white_check_mark: | :white_check_mark: | :white_check_mark:  |
| [dzen.ru](https://dzen.ru/)                                                                                      | :o:                | :o:                        | :o:                          | :o:                | :o:                | :o:                 |
| [avito.ru](https://www.avito.ru/)                                                                                | :o:                | :o:                        | :o:                          | :white_check_mark: | :white_check_mark: | :white_check_mark:  |
| [pinterest.fr](https://www.pinterest.fr/ideas/cuisine-et-boissons/93:white_check_mark:387:o:85757/)              | :white_check_mark: | :white_check_mark:         | :white_check_mark:           | :white_check_mark: | :white_check_mark: | :white_check_mark:  |
| [cloudflare.com](https://www.cloudflare.com/)                                                                    | :white_check_mark: | :white_check_mark:         | :white_check_mark:           | :white_check_mark: | :white_check_mark: | :white_check_mark:  |
| [youtube.com](https://www.youtube.com/watch?v=uUah6_-SKR8)                                                       | :white_check_mark: | :white_check_mark:         | :white_check_mark:           | :white_check_mark: | :white_check_mark: | :white_check_mark:  |
| [auchan.fr](https://www.auchan.fr/recherche?text=riz&page=2)                                                     | :white_check_mark: | :white_check_mark:         | :white_check_mark:           | :white_check_mark: | :white_check_mark: | :white_check_mark:  |
| [zara.com/fr](https://www.zara.com/fr/fr/homme-pantalons-l838.html?v:white_check_mark:=235:white_check_mark:278) | :o:                | :o:                        | :o:                          | :o:                | :o:                | :o:                 |
| [winamax.fr/paris-sportifs](https://www.winamax.fr/paris-sportifs)                                               | :o:                | :o:                        | :o:                          | :white_check_mark: | :white_check_mark: | :white_check_mark:  |

#### Statistics

- Total requests: 156
- Successful requests: 91
- Blocked requests: 65

### Areas of improvement

- Modify the function for detecting blocked requests
- Add a web client that allows the execution of javascript (curl package not strong enough for cloudflare)
- Implement AI for solving easy captchas

### Disclaimer

This project is for educational purposes only. Ensure compliance with ethical guidelines and legal regulations when conducting web fingerprinting activities.
