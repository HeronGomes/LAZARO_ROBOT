#include <Servo.h> 
 
Servo servoBoca;   
int pos = 0;    
int maximo = 60;

int comando = 0;

void setup() 
{ 
  servoBoca.attach(9); 
  servoBoca.write(pos); 
  Serial.begin(9600);
   
} 
 

void mexeBoca()
{

  for(pos; pos < maximo; pos += 4)  
  {                                  
    servoBoca.write(pos);               
    delay(15);                        
  } 
  for(pos = maximo; pos>=1; pos-= 4)     
  {                                
    servoBoca.write(pos);               
    delay(15);                        
  } 


}



void loop() 
{ 
  
    
    while (!Serial) {
    ;
    }
  
    if(Serial.available() > 0)
    {
            
      do{
        
        mexeBoca();
        comando = Serial.read();
      
      }while(comando != 48); // zero decimal
      
    }
} 
