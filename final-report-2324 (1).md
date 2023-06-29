# Final-Delivery of Software

Team ID: 2324

Team members: 12011129 黄宇航, 12011039 王开妍, 12011501 冯泉弼, 12011231 李宇轩, 12010208 易乐桐

## 1. Metrics

For back-end, we use cloc to count the lines of Code and number of source files:

For src:

![image1](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage1.png)

For whole back-end project:

![image2](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage2.png)

Lines of Code: 1264

Number of modules: 18

At the same time, we can get the number of source files and number of packages.

Number of packages: 3

Number of source files: 38

Then we use the pip freeze instruction of python and wc instruction to count the number of 3rd party dependencies:

![](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/software1685588395489.png)

number of 3rd party dependencies: 80

For maintainability of our team project, we use a tool called pylint to analyze code for normality and maintainability, to list code that doesn't conform to the specification, and to score the maintainability of the project.

Then we use pylint to score a project found in the github using flask. The project is to help developers use REST APIs with Flask and Python.

![image3](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage3.png)

Here's how pylint looks at our project.Because of the number of projects we're looking at, we can see that the final score is 4.39:

![image4_2](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage4_2.png)

From the above comparison, we can see that the maintainability of our project is not high, and we need to continue to improve the code style.

For front-end, we use git bash to count the lines of Code:

![image5](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage5.png)

Lines of Code: 3880

Number of source files: 39

Number of modules: 35

Number of packages: 5



## 2. Documentation

The documentation has been uploaded to the team's github repo and the url is below:

Documentation for end users:

https://github.com/Barry-Yellow/works/blob/94b921c1f83064151072bc40bf6e5ec54a364028/2324-User-Guide.md

Documentation for developers:

https://github.com/Barry-Yellow/works/blob/94b921c1f83064151072bc40bf6e5ec54a364028/Documentation%20for%20developers.pdf



## 3. Tests

### **3.1 tools:** 

 ● Unit Test & IT: pytest & coverage

 ● End-to-End Test: postman & frontend app

### **3.2 Unit Test & IT**

We use pytest to test each branch and the corresponding url route. In each test we set a list of parameters and then GET/POST these data in json to the route we want to test. After the app return response, we get the data from it and assert if it's in expected. 

As for coverage report, we use coverage to generate a report. The coverage report can be seen in the GitHub link https://github.com/Barry-Yellow/test/blob/8b7c8fb476b359e8fa57e5d6f447d6cde94625b8/TeamProject/htmlcov/index.html 

**source code of test:** 
link :https://github.com/Barry-Yellow/test.git

**code screenshot:**![image13](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage13.png)

| ![image14](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage14.png) | ![image15](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage15.png) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![image6](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage6.png) | ![image16](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage16.png) |

**result screenshot:**

![image17](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage17.png)

![image8](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage8.png)

The coverage report can be seen in the GitHub link https://github.com/Barry-Yellow/test/blob/8b7c8fb476b359e8fa57e5d6f447d6cde94625b8/TeamProject/htmlcov/index.html 

### **3.3 End-to-End test**

We wrote URLs in postman, so that we can simply configure the parameters in HTTP body or somewhere in some certain format. As shown below, we can send GET/POST method to test our interface, and then check the response.

![image18](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage18.png)



## **4. Build**

###### **Part I**

The packaging tool I use is PyInstaller. PyInstaller is a tool used to package Python applications into standalone executable files. It can package Python code and its dependencies into a single executable file, eliminating the need to install the Python interpreter or other dependencies on the user's computer.

With PyInstaller, you can convert Python applications into executable files that can run on different platforms such as Windows, Mac, and Linux. It supports packaging Python code into a single executable file or folder, and it can automatically handle the required dependencies for running on different systems.

###### **Part II**

The command for building our program is:
```
pyinstaller main.py -F
```
PyInstaller performs the following tasks during the build process:

1. Import Analysis: PyInstaller analyzes the Python source code or script to determine which modules are imported and used.

2. Module Collection: Based on the import analysis results, PyInstaller collects all the modules and related resource files that are being used.

3. Module Analysis: The collected modules are further analyzed by PyInstaller to understand the dependencies between the modules.

4. Handling Data Files: PyInstaller processes the data files used in the application, such as images, audio, or other resource files.

5. Generating the Executable: In the final stage of the build process, PyInstaller packages all the modules and resource files together to generate a standalone executable file.

6. Resolving Dependencies: PyInstaller automatically resolves the dependencies required by the application, including Python modules, third-party libraries, and other resource files.

7. Generating the Bootloader Script: PyInstaller also generates a bootloader script that is responsible for starting the application and setting up the necessary runtime environment.

After a successful build using PyInstaller (using the aforementioned command), it will generate two folders in the current directory: "build" and "dist".

The "build" folder contains information related to the build process, such as temporary files, logs, and intermediate artifacts generated during the build.

The "dist" folder, on the other hand, contains the final output of the build process. It typically includes the generated standalone executable file, along with any required resources or dependencies needed for the application to run independently on the target system.

It's worth noting that the specific contents of the "build" and "dist" folders may vary depending on the options and configurations used during the PyInstaller build process.

###### **Part III**

The command for building our program is:

```
pyinstaller main.py -F
```

No additional compilation script is required. This is a screen shot of a successful compilation

![image9](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage9.png)

## **5. Deployment**

###### **Part I**

The project containerization technology I'm using is Docker. Docker is a containerization deployment technology that provides a lightweight solution for packaging applications and their dependencies into independent containers. This allows them to be deployed and run in different environments without concerns about environmental differences.

With Docker, you can create an image that includes the application, its related configurations, libraries, and dependencies. This image can be deployed and run in any Docker-supported environment, including development machines, testing environments, and production servers. Docker containers provide an isolated runtime environment that ensures consistent behavior of the application across different environments.

###### **Part II**

This is the Dockerfile I use, before using docker, I need to generates a list of dependencies for a python project. The command I used to generate the requrements.txt is：

```
pipreqs . --encoding=utf8
```

###### **Part III**

![image7](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage7.png)

![](https://cdn.jsdelivr.net/gh/lyxqi7/Image@main/softwareimage19.png)

###### **Part IIII**
For front-end:

Clone the front-end project from https://github.com/YuuKiriyama/final_front_end

Set up the environment of react-native, nodejs, npm and yarn.

Download Expo Go from App store or Google Play on your mobile device.

Run command yarn start.

Make sure the mobile device and your server under the same subnet.

Scan the QR code on the terminal with Expo Go, then you can see the front-end preview.
