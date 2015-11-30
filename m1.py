/*











 */



#include <stdio.h>

#include <stdlib.h>

#include <string.h>

#include <math.h>





struct io_header_1 {

  int      npart[6];

  double   mass[6];

  double   time;

  double   redshift;

  int      flag_sfr;

  int      flag_feedback;

  int      npartTotal[6];

  int      flag_cooling;

  int      num_files;

  double   BoxSize;

  double   Omega0;

  double   OmegaLambda;

  double   HubbleParam; 

  char     fill[256- 6*4- 6*8- 2*8- 2*4- 6*4- 2*4 - 4*8];  //--- Fills to 256 Bytes 

} header1;



//===============================================================

//--- Global variables

//===============================================================

int     nPart;

double *density;

double *tetraden;

int    *tetras;



struct particle_data {

  double  Pos[3];

} *P;     //--- Pointer to structure



//===============================================================

//================   FUNCTIONS DECLARATION  =====================

//===============================================================

void allocate_memory(void);

void load_snapshot(char *fname, int files);

long get_densities(float x,float y,float z, float win);

void save_density(char *fname);





//===============================================================

//

//===============================================================

int main(int argc, char **argv)

{



  if (argc != 6)

    {

      printf("<-----------------------------------------------------------> \n");

      printf("Usage: \n");

      printf("       ./snap_sample_tophat_particles x y z tophat_radius\n");

      printf("       Return tophat particles inside window at a given position. Non-periodic\n");      

      printf("       \n");

      printf("       \n");

      printf("       \n");

      printf("       \n");

      printf("       \n");

      printf("       \n");

      printf("<-----------------------------------------------------------> \n");

      exit(0);

    }



  //--- Read Gadget file

  load_snapshot(argv[1], 1);



  long dummy = get_densities(atof(argv[2]), atof(argv[3]), atof(argv[4]), atof(argv[5]));



  free(density);

  free(P);



  return(0);



}



//==================================================================

//           FUNCTIONS

//==================================================================





//----------------------------------------------------------

//

//----------------------------------------------------------

long get_densities(float x, float y, float z, float win){

  long  i, cont=0;

  float dista;



  float win2 = win*win;



  //--- Get particles inside window

  for(i=0; i<nPart; i++){    

    dista = (P[i].Pos[0]-x)*(P[i].Pos[0]-x) + (P[i].Pos[1]-y)*(P[i].Pos[1]-y) + (P[i].Pos[2]-z)*(P[i].Pos[2]-z);

    if (dista <= win2) {

      printf("%f,%f,%f\n", P[i].Pos[0],P[i].Pos[1],P[i].Pos[2]);

      cont++;

    }



  }



  return cont;

} //--- end get_densities()







//----------------------------------------------------------

//--- Loads particle data from Gadget's default file

//----------------------------------------------------------

void load_snapshot(char *fname, int files) {

#define SKIP fread(&dummy, sizeof(dummy), 1, fd);

  FILE *fd;

  char buf[200];

  int  i,k,dummy,ntot_withmasses;

  int  n,pc,pc_new;

  int  count_err=0;

  

  sprintf(buf,"%s",fname);      

  if(!(fd=fopen(buf,"r"))){

    printf("can't open file '%s'\n",buf);

    exit(0);

  }

  

  //--- Reader header

  SKIP;

  fread(&header1, sizeof(header1), 1, fd);  //--- Read Header1 in one pass

  SKIP;



  nPart = header1.npart[1];



  //--- Allocate memory for particles

  allocate_memory();

  

  //--- Read Particle's positions

  SKIP;

  float tempf3[3];

  for(n=0;n<header1.npart[1];n++) {

    fread(&tempf3, sizeof(float), 3, fd);

    P[n].Pos[0] = (double) tempf3[0];

    P[n].Pos[1] = (double) tempf3[1];

    P[n].Pos[2] = (double) tempf3[2];

  }

  SKIP;



  fclose(fd);

  

  //--- Fix boundaries (x >= BoxSize || x < 0)

  //  printf("   Checking periodic conditions...\n");

  for(i=0; i<header1.npart[1]; i++){

    if(P[i].Pos[0] >=  header1.BoxSize){ P[i].Pos[0] = P[i].Pos[0] -  header1.BoxSize; count_err++;}

    if(P[i].Pos[1] >=  header1.BoxSize){ P[i].Pos[1] = P[i].Pos[1] -  header1.BoxSize; count_err++;}

    if(P[i].Pos[2] >=  header1.BoxSize){ P[i].Pos[2] = P[i].Pos[2] -  header1.BoxSize; count_err++;}

    if(P[i].Pos[0] <               0.0){ P[i].Pos[0] = P[i].Pos[0] +  header1.BoxSize; count_err++;}

    if(P[i].Pos[1] <               0.0){ P[i].Pos[1] = P[i].Pos[1] +  header1.BoxSize; count_err++;}

    if(P[i].Pos[2] <               0.0){ P[i].Pos[2] = P[i].Pos[2] +  header1.BoxSize; count_err++;}

  }

  

  //printf("   %d particles out of box\n", count_err);

  



} //--- end load_snapshot()





//----------------------------------------------------------

//

//----------------------------------------------------------

void save_density(char *fname) {

  FILE *fd;

  char buf[256];

  int  i;



  //--- Load filename

  sprintf(buf,"%s.lden",fname);

  

  fd=fopen(buf,"wb");

  //--- Header of file (number of partices)

  fwrite(&nPart,sizeof(int),1,fd);

  fclose(fd);



} //--- end save_density()







//----------------------------------------------------------

//---Allocates the memory for the particle data.

//----------------------------------------------------------

void allocate_memory(void) {

  //printf("   Allocating memory for %d particles...",header1.npart[1] );

  

  if(!( P = (particle_data *) malloc(header1.npart[1]*sizeof(struct  particle_data) ))){

      fprintf(stderr,"failed to allocate memory HIGH RES.\n");

      exit(0);

    }



  if(!( density = (double *) malloc(header1.npart[1]*sizeof( double ) ))){

    fprintf(stderr,"failed to allocate memory density vertices.\n");

    exit(0);

  }



  //--- 6 times the number of cells (particles)

  if(!( tetraden = (double *) malloc(header1.npart[1]*6*sizeof( double ) ))){

    fprintf(stderr,"failed to allocate memory for tetrahedra density.\n");

    exit(0);

  }



  for (int i=0; i<header1.npart[1];i++) density[i]=0;





} //--- end  allocate_memory()
