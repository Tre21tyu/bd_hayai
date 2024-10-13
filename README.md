#<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
<a href="https://github.com/github_username/repo_name">
<img src="images/logo.png" alt="Logo" width="80" height="80">
</a>

<h3 align="center">bd_hayai</h3>

<p align="center">
project_description
<br />
<a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
<br />
<br />
<a href="https://github.com/github_username/repo_name">View Demo</a>
·
<a href="https://github.com/github_username/repo_name/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
·
<a href="https://github.com/github_username/repo_name/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
</p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
<summary>Table of Contents</summary>
<ol>
<li>
<a href="#about-the-project">About The Project</a>
<ul>
<li><a href="#built-with">Built With</a></li>
</ul>
</li>
<li>
<a href="#getting-started">Getting Started</a>
<ul>
<li><a href="#prerequisites">Prerequisites</a></li>
<li><a href="#installation">Installation</a></li>
</ul>
</li>
<li><a href="#usage">Usage</a></li>
<li><a href="#roadmap">Roadmap</a></li>
<li><a href="#contributing">Contributing</a></li>
<li><a href="#license">License</a></li>
<li><a href="#contact">Contact</a></li>
<li><a href="#acknowledgments">Acknowledgments</a></li>
</ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Medimzier is cursed with a frontend is egregiously slow, lacking in functionality, many years outdated. Medimizer, however, is also a SQL database. We can use this to our advantage to implement really cool functionanlity outside of it. One of these functions in MM is the poweradd function... We should be able to power add from excel files and csv files, however we cant. Medimizer software is proprietary and so we can't make direct modifications to the front end or update it or asking the company for large amounts of money. One good solution is to generate python code that enables us to filter, clean, and process our excel sheets into SQL code that can be entered via SSMS. 

One feature of MM software, invaluble for larger projects completed in the hospital is the Power add function. This function allows large numbers of equipment to be batch added to the CMMS. Unfortunately, the Poweradd function is lacking in both speed and functionality. The UI does not allow for easy copying of data down columns or rows, blah blah 

`bd_hayai`; BD derivered from the project from which this script saw its conception, and hayai coming from the Japanese meaning fast, is the first of many attempts to improve this process. Microsoft excel offers more liberties when it comes to file creation and copying data down columns as well as providing funcitonality and rulesets to how data is taken. The pandas library allows for the processing of data from the excel sheet and into SQL code.

Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

* [![Python][python]]
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Run
Navigate to the hayai folder in your CLI and run
```bash
pip install hayai .
```


### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

<!-- USAGE EXAMPLES -->
## Usage

### Copying the template sheet

The template sheet contains the replicable starter excel sheet into which BD alaris data will be entered into. 

The end user can invoke this fucntion by using the `cpysrc` function
```bash
hayai cpysrc
```

This generates a new hayai table which will then be used in step1 and step2. It will be `num` + `はやい`.csv where the num is number of csv files alreadyin the thing

### STEP 1: Pulling the MEKs from the CMMS
Each piece of equipment has a unique master encryption key(MEK). These are based on the hospitals local asset number, AKA 'Control number' In order to modify attributes of the equipment, the keys must be pulled from the CMMS. After processing the data in `はやい.csv` file, we can systematically query these keys to be pulled by generating custom SQL.

We can do this as follows.
```bash
hayai step1 arg1.csv
```

Where arg1.csv is the hayai file

Result:
```sql
SELECT
        [EquipmentKey],
        [CN],
        [CycleDate],
        [CycleSetBy],
        [RTLSCode]
    FROM
        [URMCCEX3].[dbo].[Equipment]
    WHERE 
        [ControlNo] IN (
'00108992', '00108993', ...  
        )
    ORDER BY 
        CASE
            WHEN [ControlNo] = '00108992' THEN 1
            WHEN [ControlNo] = '00108993' THEN 2
    END;
```
### STEP 2: Generating SQL to be added into the CMMS via SSMS
Once we have the MEKs, we can use them to finalize changes in our original hayai table and add them to the CMMS in one step. 

We can do this as follows
```bash
hayai step2 arg1.csv arg2.csv
```

Where `arg1.csv` is our original `はやい.csv` file, and `arg2.csv` is our csv file containing the MEK data.

Result:
```sql
UPDATE [URMCCEX3].[dbo].[Equipment]
    SET 
        CycleSetBy = 'Equipment',
        CycleDate = CASE
           WHEN [EquipmentKey] = 266943 THEN '1991-09-01 00:00:00.000'
           WHEN [EquipmentKey] = 266696 THEN '1991-09-01 00:00:00.000'
           WHEN [EquipmentKey] = 266696 THEN '1991-09-01 00:00:00.000'
        END,
    [RTLScode] = CASE
        WHEN [EquipmentKey] = 266943 THEN '000CCC14E6F6'
        WHEN [EquipmentKey] = 266696 THEN '000CCC11B021'
        WHEN [EquipmentKey] = 266626 THEN '000CCC11AE7B'
        ...
    END
    WHERE 
       [EquipmentKey] IN ('266943', '266696', '266626' ...);
```
### `-c` and `-l` arguments
#### `-c` - Copying SQL to the clipboard 
The SQL code will be customarily output to the terminal. It is possible, however, for the resulting SQL code to be copied to the clipboard directly with the -c argument as follows
```bash
hayai step1 arg1.csv -c
```

Result should be the same as the above, however the below should print to the console
```bash
SQL command copied to clipboard!
```

#### `-l` - Displaying the Dataframes in the terminal
When the excel sheet is processed by pandas, it will exist periodically as a dataframe for the purposes of filtering, cleaning, and processing the data. To verify that this process worked, the `l` argument can be invoked as shown below

```bash
hayai step1 arg1.csv -l
```

Result
```bash
          CN CYCLESTARTDATE          RTLS
0   00108992     1991-09-01  000CCC14E6F6
1   00108993     1991-09-01  000CCC11B021
2   00108994     1991-09-01  000CCC11AE7B
3   00108995     1991-09-01  000CCC119C83
4   00108284     1991-09-01  000CCC120345
```

```bash
hayai step2 arg1 arg2.csv -l
```

Result
```bash
          CN CYCLESTARTDATE  ...     MEK       CN_
0   00108992     1991-09-01  ...  266943  00108992
1   00108993     1991-09-01  ...  266696  00108993
2   00108994     1991-09-01  ...  266626  00108994
3   00108995     1991-09-01  ...  266704  00108995
4   00108284     1991-09-01  ...  266574  00108284
```

`_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/github_username/repo_name/graphs/contributors">
<img src="https://contrib.rocks/image?repo=github_username/repo_name" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
