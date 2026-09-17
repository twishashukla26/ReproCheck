# **ReproCheck**

###### 

###### An Open-Source Reproducibility Auditor for Data Science and Software Projects



ReproCheck is a lightweight open-source tool that inspects a project repository and identifies common issues that may prevent the project from being reproduced on another machine.



## Problem



A project repository may contain source code, dependencies, datasets and documentation, but these files do not always guarantee that another user can successfully run the project.



##### Common reproducibility problems include:



\- Missing dependency files

\- Missing referenced files

\- Hard-coded local paths

\- Missing documentation

\- Missing or invalid containerisation configuration



ReproCheck aims to automatically identify these issues and generate a clear reproducibility report.



## Objectives



\- Inspect the structure of a project repository.

\- Check for important documentation and configuration files.

\- Analyse Python dependencies.

\- Detect missing referenced files.

\- Detect hard-coded absolute paths.

\- Check Docker and Docker Compose configuration.

\- Generate a reproducibility report.

\- Provide a reproducible execution environment using containers.



## Planned Workflow



```text

Target Project

&#x20;     |

&#x20;     v

Project Scanner

&#x20;     |

&#x20;     +---- Structure Checks

&#x20;     |

&#x20;     +---- Dependency Checks

&#x20;     |

&#x20;     +---- File \& Path Checks

&#x20;     |

&#x20;     +---- Container Checks

&#x20;     |

&#x20;     v

Result Engine

&#x20;     |

&#x20;     v

Reproducibility Report

---


Technology Stack
---

* Python
* Git
* GitHub
* Linux / Git Bash
* Docker
* Docker Compose
* Pytest
* Rich
* PyYAML



## Project Status



Currently under development.



## Project Structure

reprocheck/

├── reprocheck/

├── tests/

├── benchmark\_projects/

├── reports/

├── docs/

├── README.md

├── requirements.txt

├── .gitignore

└── LICENSE

**License**



This project is released under the MIT License.







