void getData();
void printData();

uint8_t x;
uint8_t data[12];
bool newData = 0;
int index;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial1.begin(9600);

  Serial.println("Starting serial read test.");
}

void loop() {
  getData();
  if(newData){
    printData();
  }
  
}

void getData(){
  if( Serial1.available() ){
    x = Serial1.read(); // Reads incoming byte, 8-bit data fits this well.
    if( x == 0xFF ){
      Serial.println(index);
      index = 0; // Start bit detected, filling up data from the start.
//      Serial.println("New stream started");
    } else {
      if(index < 12){
        data[index] = x;
//        Serial.print(data[index], HEX);
//        Serial.print(" gotten at index ");
//        Serial.println(index);
        if (index==11) {
          //Data frame complete
          newData=true; // We have managed to update 12 values.
        } 
        index++;
      } else {
        Serial.println("Data frame overrun");
      }
    }
  }
}

void printData(){
  Serial.print("Data received ");
  for(int i=0; i<12; i++){
    Serial.print(data[i], HEX);
    Serial.print(" ");
  }
  Serial.println();
  newData = false;
}
