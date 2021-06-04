# How to Run Julia on SageMaker

## Outlines:
*   What is Amazon SageMaker, and Why you should use it?
*   Make your notebook instance with Julia.
*   Automation with CloudForamtion

## What is Amazon SageMaker, and Why you should use it?

Amazon [SageMaker](https://aws.amazon.com/sagemaker/) is a fully managed service that provides every developer and data scientist with the ability to quickly build, train, and deploy machine learning (ML) models rapidly and without the need to worry about infrastructure. Julia is a high-level, high-performance, dynamic programming language. While it is a general-purpose language and can be used to write any application, many of its features are well suited for numerical analysis and computational science. By Merging Julia with SageMaker, you will be able to get the most out of Julia as you can easily access high-performance instances.

## Make your notebook instance with Julia

An Amazon SageMaker [notebook instance](https://docs.aws.amazon.com/sagemaker/latest/dg/nbi.html) is a machine learning (ML) compute instance running the Jupyter Notebook App. SageMaker manages creating the instance and related resources. Use Jupyter notebooks in your notebook instance to prepare and process data, write code to train models, deploy models to SageMaker hosting, and test or validate your models. You can make multiple notebooks within your notebook instance.

To make a notebook instance, you should go to Notebook instance in SageMaker part of the AWS console, then click on the Create Notebook instance button:



<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image1.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image1.png "image_tooltip")


On the following page, you should define the configuration of your notebook instance:

1- Notebook instance name

2- Notebook instance type: 

The type instance that will be used to run your notebook within this instance. for more information on choosing instance type, see [here](https://datachef.co/blog/how-to-choose-the-best-training-instance-on-sagemaker/).

3- Volume size in GB:

The available storage to your notebook instance.



<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image2.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image2.png "image_tooltip")


In default Configuration, SageMaker doesn’t have Julia as a kernel for notebooks, so we should install and add it to SageMaker; we do it in the** Lifecycle Configuration **part of this page. A [lifecycle configuration](https://docs.aws.amazon.com/sagemaker/latest/dg/notebook-lifecycle-config.html) provides shell scripts that run only when you create the notebook instance or whenever you start one.

1- Click on **Lifecycle Configuration **and select the** Create a new lifecycle configuration**.



<p id="gdcalert3" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image3.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert4">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image3.png "image_tooltip")


2- Choose a name for Lifecycle Configuration.

3- Paste this script in the **Create Notebook** part, this script will insatll and activate Julia in the first start of your notebook instance:

```bash

#!/bin/bash

set -e

sudo -u ec2-user -i &lt;<EOF

echo ". /home/ec2-user/anaconda3/etc/profile.d/conda.sh" >> ~/.bashrc 

conda create --yes --prefix ~/SageMaker/envs/julia

curl --silent https://julialang-s3.julialang.org/bin/linux/x64/1.6/julia-1.6.0-linux-x86_64.tar.gz | tar xzf -

cp -R julia-1.6.0/* ~/SageMaker/envs/julia/

mkdir -p ~/SageMaker/envs/julia/etc/conda/activate.d

echo 'export JULIA_DEPOT_PATH=~/SageMaker/envs/julia/depot' >> ~/SageMaker/envs/julia/etc/conda/activate.d/env.sh

echo -e 'empty!(DEPOT_PATH)\npush!(DEPOT_PATH,raw"/home/ec2-user/SageMaker/envs/julia/depot")' >> ~/SageMaker/envs/julia/etc/julia/startup.jl

conda activate /home/ec2-user/SageMaker/envs/julia

julia --eval 'using Pkg; Pkg.add("IJulia"); using IJulia'

EOF

```

4- Paste this script in the **Start Notebook** part, this script will activate Julia each time you start your notebook instance:

```bash

#!/bin/bash

set -e

sudo -u ec2-user -i &lt;<EOF

echo ". /home/ec2-user/anaconda3/etc/profile.d/conda.sh" >> ~/.bashrc

conda run --prefix ~/SageMaker/envs/julia/ julia --eval 'using IJulia; IJulia.installkernel("Julia")'

EOF

```

5- Click on **Create Configuration** button.

6- Now, you can leave other settings as default and click on **Create notebook instance**.

Your notebook instance will be ready to use in minutes; the first time you start the instance or install any Julia package will take some time but will be so much faster in the next use.

## Automation with CloudForamtion

This whole process can be automated through an Amazon CloudFormation template. To create the notebook in this way, follow this procedure:

1- Download the CloudFormation template from [here](https://github.com/myprogrammerpersonality/JuliaOnSageMaker/blob/main/julia1.6-notebook.yaml).

2- Go to the CloudFormation part of the AWS console.

3- On the stacks section, click on Create Stack / From new resources (standard).

4- Choose the **Template is ready** and **Upload a template file** option and upload the downloaded template.

5- Click **Next**.

6- Choose a name for the stack and also the notebook instance name and type, also specify volume size.

7- Click **Next** for this page and the next one.

8- Check the **I acknowledge that AWS CloudFormation might create IAM resources**.

9- Click **Create stack**.

CloudFormation will make a notebook instance for you along with Lifecycle configuration. You will always can delete the whole created resources with the Delete option of the stack.
