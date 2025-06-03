2 GUIDES:
GUIDE 1 HVIS MAN IKKE HAR KØRT DET FØR
GUIDE 2 HVIS MAN HAR KØRT DET FØR

GUIDE 1

1. Hav DOCKER DESKTOP installeret

2. Åben en cmd/Desktop-terminal eller en anden terminal.

3. Kør følgende linje: cd "C:\STUDIE\4. Semester\Dataprojekt\Pipeline\docker_detectron2_env" Tilpas den til hvor du har DOCKER filen "Dockerfile_pytorch3d_jupyter" liggende

4. Byg docker med følgende linje i terminalen: docker build -t pytorch3d_jupyter:detectron2_installed -f Dockerfile_pytorch3d_jupyter .

5. kopier stien der minder om: http://127.0.0.1:8888/lab og åben det i din browser


GUIDE 2


1. HAR du bygget docken før, så kør følgende i terminalen inde i DOCKER DESKTOP:

cd "C:\STUDIE\4. Semester\Dataprojekt\Pipeline\docker_detectron2_env" eller hvor du har "Dockerfile_pytorch3d_jupyter" liggende

2. Kør Dockeren med følgende kommanda i terminalen:

2.1 docker run -p 8888:8888 -it pytorch3d_jupyter:detectron2_installed

2.2 Eller med en mappe: docker run -p 8888:8888 -v C:\Users\tueme\some-folder:/home/user/app -it pytorch3d_jupyter:detectron2_installed

f.eks. docker run -p 8888:8888 -v "C:\STUDIE\4. Semester\Dataprojekt\Dataprojekt\Pipeline:/home/user/app" -it pytorch3d_jupyter:detectron2_installed


