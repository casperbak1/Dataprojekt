2 GUIDES:
GUIDE 1 HVIS DU IKKE HAR KØRT DET FØR
GUIDE 2 HVIS DU HAR

GUIDE 1

1. Hav DOCKER DESKTOP installeret

2. Åben en cmd/git Bash/Docker Desktop terminal eller en anden terminal.

3. cd "C:\STUDIE\4. Semester\Dataprojekt\Pipeline\docker_detectron2_env" eller hvor du har DOCKER filen liggende

4. Byg docker: docker build -t pytorch3d_jupyter:detectron2_installed -f Dockerfile_pytorch3d_jupyter .

5. kopier stien der minder om: http://127.0.0.1:8888/lab og åben det i din browser


GUIDE 2


1. HAR du bygget docken før, så kør følgende i terminalen inde i DOCKER DESKTOP:

cd "C:\STUDIE\4. Semester\Dataprojekt\Pipeline\docker_detectron2_env" eller hvor du har "Dockerfile_pytorch3d_jupyter" liggende

docker run -p 8888:8888 -it pytorch3d_jupyter:detectron2_installed

Eller med en mappe: docker run -p 8888:8888 -v C:\Users\tueme\some-folder:/home/user/app -it pytorch3d_jupyter:detectron2_installed

f.eks. docker run -p 8888:8888 -v "C:\STUDIE\4. Semester\Dataprojekt\Pipeline\Pipeline:/home/user/app" -it pytorch3d_jupyter:detectron2_installed


docker run -p 8888:8888 -v "C:\STUDIE\4. Semester\Dataprojekt\Dataprojekt\Pipeline:/home/user/app" -it pytorch3d_jupyter:detectron2_installed


