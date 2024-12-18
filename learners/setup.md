---
title: Setup
---

## Files

You need to download some files to follow this lesson:

1. Download [scons-lesson.zip][zip-file].

2. Move `scons-lesson.zip` into a directory which you can access via your bash shell.

3. Open a Bash shell window.

4. Navigate to the directory where you downloaded the file.

5. Unpack `scons-lesson.zip`:

  ```source
  $ unzip scons-lesson.zip
  ```

6. Change into the `scons-lesson` directory:

  ```source
  $ cd scons-lesson
  ```

## Software

You also need to have the following software installed on your computer to follow this lesson. The
recommeneded approach is to create a
[Conda](https://docs.conda.io/projects/conda/en/latest/index.html) virtual environment for this
lesson.

```
$ conda create --name scons-lesson python scons numpy matplotlib
$ conda activate scons-lesson
```

### SCons

[SCons](https://scons.org/) can be installed with the [pip](https://pip.pypa.io/en/stable/) or
[Conda](https://docs.conda.io/projects/conda/en/latest/index.html) package managers.

### Python

Python2 or Python3, Numpy and Matplotlib are required.
They can be installed separately, but the easiest approach is to install
[Anaconda](https://www.anaconda.com/distribution/) which includes all of the
necessary python software.

[zip-file]: files/scons-lesson.zip
