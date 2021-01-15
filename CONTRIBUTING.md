## Contributing

### Typos/Bugs/Fixes

If you find any bugs/typos/improvements you'd like to suggest to our work, please open an issue on the [Github repository](https://github.com/UBC-MDS/happy-dash/issues). It's also helpful if you can double check the issue hasn't already been raised in any existing issues.

Please ensure you create a minimal reprex of any bugs you find - this will help us fix it faster!

### Contributions

If you want to add code contributions yourself please follow the steps below to configure a development environment. Before starting on major new work - please run the idea by the maintainer team by opening an issue on the Github repo.

All contributors must abide by our [code of conduct](CODE_OF_CONDUCT.md).

## Environment Setup

After cloning this GitHub repository, install the required conda dependencies by configuring a conda environment for this repo. From the root of the repo run:

```
$ conda env create
$ conda activate happydash
```

For the R scripts, open the Rstudio `.Rproj` file in Rstudio. From the console run:

```
renv::restore()
```

All R package versions can be found in `renv.lock`.

### Workflow for Pull Requests

We use the fork methodology for accepting pull requests.