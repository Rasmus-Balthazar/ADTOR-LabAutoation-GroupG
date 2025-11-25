#include <Arduino.h>
#include <CmdMessenger.h>
#include "dataModel.h"
#include "df4MotorDriver.h"
#include <SparkFun_AS7343.h>

CmdMessenger cmdMessenger(Serial, ',', ';', '/');

SfeAS7343ArdI2C mySensor;

uint16_t myData[ksfAS7343NumChannels]; // Array to hold spectral data

// This is the list of recognized commands. These can be commands that can either be sent or received.
// In order to receive, attach a callback function to these events
void OnUnknownCommand();
void OnWatchdogRequest();
void OnArduinoReady();
void OnGetState();
void OnGetLastStep();
void OnReceiveStep();
void OnReceiveStop();
void GetSensorReadings();

void returnState();
void returnLastStep();
void receiveStep();
void receiveStop();

enum
{
  // Commands
  kWatchdog,              // Command to request application ID
  kAcknowledge,           // Command to acknowledge a received command
  kError,                 // Command to message that an error has occurred
  kGetState,              // Command to get the pump states
  kGetStateResult,        // Command to send the full state of the pumps
  kGetLastStep,           // Command to get the current step
  kGetLastStepResult,     // Command to send the current step
  kStep,                  // Command to receive a step (pump state + time), should always contain the full state of the pumps
  kStop,                  // Command to stop all pumps
  kStepDone,              // Command to signal a step done
  kGetSensorReadings,     // Command to get sensor readings
  sensorReadingsResponse, // Response to get sensor readings
};

// Commands we send from the PC and want to receive on the Arduino.
// We must define a callback function in our Arduino program for each entry in the list below.
void attachCommandCallbacks()
{
  // Attach callback methods
  cmdMessenger.attach(OnUnknownCommand);
  cmdMessenger.attach(kWatchdog, OnWatchdogRequest);
  cmdMessenger.attach(kGetState, OnGetState);
  cmdMessenger.attach(kGetLastStep, OnGetLastStep);
  cmdMessenger.attach(kStep, OnReceiveStep);
  cmdMessenger.attach(kStop, OnReceiveStop);
  cmdMessenger.attach(kGetSensorReadings, GetSensorReadings);
}

// ------------------  C A L L B A C K S -----------------------

// Called when a received command has no attached function
void OnUnknownCommand()
{
  cmdMessenger.sendCmd(kError, "Command without attached callback");
}

void OnWatchdogRequest()
{
  // Will respond with same command ID and Unique device identifier.
  cmdMessenger.sendCmd(kWatchdog, "0000000-0000-0000-0000-00000000001");
}

// Callback function that responds that Arduino is ready (has booted up)
void OnArduinoReady()
{
  cmdMessenger.sendCmd(kAcknowledge, "Arduino ready");
}

void OnGetState()
{
  returnState();
}

void OnGetLastStep()
{
  returnLastStep();
}

void OnReceiveStep()
{
  receiveStep();
}

void OnReceiveStop()
{
  receiveStop();
}

void GetSensorReadings()
{
  uint16_t blue = mySensor.getBlue();
  uint16_t red = mySensor.getRed();
  uint16_t green = mySensor.getGreen();

  cmdMessenger.sendCmdStart(sensorReadingsResponse);
  cmdMessenger.sendCmdBinArg<uint16_t>(red);
  cmdMessenger.sendCmdBinArg<uint16_t>(green);
  cmdMessenger.sendCmdBinArg<uint16_t>(blue);

  cmdMessenger.sendCmdEnd();
}

void setup()
{

  Serial.begin(115200);
  setupPumps();

  //  Do not print newLine at end of command,
  //  in order to reduce data being sent
  cmdMessenger.printLfCr(false);

  // Attach my application's user-defined callback methods
  attachCommandCallbacks();

  Serial.println("AS7343 Example 02 - All Channels");

  Wire.begin();

  // Initialize sensor and run default setup.
  if (mySensor.begin() == false)
  {
    Serial.println("Sensor failed to begin. Please check your wiring!");
    Serial.println("Halting...");
    while (1)
      ;
  }

  Serial.println("Sensor began.");

  // Power on the device
  if (mySensor.powerOn() == false)
  {
    Serial.println("Failed to power on the device.");
    Serial.println("Halting...");
    while (1)
      ;
  }
  Serial.println("Device powered on.");

  // Set the AutoSmux to output all 18 channels
  if (mySensor.setAutoSmux(AUTOSMUX_18_CHANNELS) == false)
  {
    Serial.println("Failed to set AutoSmux.");
    Serial.println("Halting...");
    while (1)
      ;
  }
  Serial.println("AutoSmux set to 18 channels.");

  // Enable Spectral Measurement
  if (mySensor.enableSpectralMeasurement() == false)
  {
    Serial.println("Failed to enable spectral measurement.");
    Serial.println("Halting...");
    while (1)
      ;
  }
  Serial.println("Spectral measurement enabled.");

  cmdMessenger.sendCmd(kAcknowledge, "Arduino has started!");
}

void loop()
{
  cmdMessenger.feedinSerialData();
  if (currentStep.state)
  {
    // Serial.println("Entering queue");
    if (!currentStep.done)
    {
      // Serial.println("Step not done");
      if (millis() - currentStep.stepStartTime >= currentStep.time)
      {
        currentStep.done = true;
        stopPumps();
        cmdMessenger.sendCmd(kStepDone);
      }
    }
    else
    {
      currentStep.state = false;
      Serial.println("Deactivating queue and clearing after done");
    }
  }
  
  mySensor.ledOn();
  // Read all data registers
  // if it fails, print a failure message and continue
  if (mySensor.readSpectraDataFromSensor() == false)
  {
      Serial.println("Failed to read spectral data.");
  }

  mySensor.ledOff();

  // Get the data from the sensor (all channels)
  // Note, we are using AutoSmux set to 18 channels
  // and the data will be written to the myData array
  // The size of the array is defined in the header file
  // This method returns the number of channels read
  int channelsRead = mySensor.getData(myData);
}

void returnState()
{
  cmdMessenger.sendCmdStart(kGetStateResult);

  cmdMessenger.sendCmdBinArg<bool>(pumpA.state);
  cmdMessenger.sendCmdBinArg<uint16_t>(pumpA.speed);
  cmdMessenger.sendCmdBinArg<bool>(pumpA.dir);

  cmdMessenger.sendCmdBinArg<bool>(pumpB.state);
  cmdMessenger.sendCmdBinArg<uint16_t>(pumpB.speed);
  cmdMessenger.sendCmdBinArg<bool>(pumpB.dir);

  cmdMessenger.sendCmdBinArg<bool>(pumpC.state);
  cmdMessenger.sendCmdBinArg<uint16_t>(pumpC.speed);
  cmdMessenger.sendCmdBinArg<bool>(pumpC.dir);

  cmdMessenger.sendCmdEnd();
}

void returnLastStep()
{

  cmdMessenger.sendCmdStart(kGetLastStepResult);

  cmdMessenger.sendCmdBinArg<bool>(currentStep.state);
  cmdMessenger.sendCmdBinArg<bool>(currentStep.done);
  cmdMessenger.sendCmdBinArg<unsigned long>(currentStep.time);

  cmdMessenger.sendCmdBinArg<bool>(currentStep.stateA);
  cmdMessenger.sendCmdBinArg<uint16_t>(currentStep.speedA);
  cmdMessenger.sendCmdBinArg<bool>(currentStep.dirA);

  cmdMessenger.sendCmdBinArg<bool>(currentStep.stateB);
  cmdMessenger.sendCmdBinArg<uint16_t>(currentStep.speedB);
  cmdMessenger.sendCmdBinArg<bool>(currentStep.dirB);

  cmdMessenger.sendCmdBinArg<bool>(currentStep.stateC);
  cmdMessenger.sendCmdBinArg<uint16_t>(currentStep.speedC);
  cmdMessenger.sendCmdBinArg<bool>(currentStep.dirC);

  cmdMessenger.sendCmdEnd();
}

void receiveStep()
{

  if (currentStep.state && !currentStep.done)
  {
    // Read and empyy cmd messenger - we are busy and dont care
    cmdMessenger.readBinArg<bool>();
    cmdMessenger.readBinArg<uint16_t>();
    cmdMessenger.readBinArg<bool>();

    cmdMessenger.readBinArg<bool>();
    cmdMessenger.readBinArg<uint16_t>();
    cmdMessenger.readBinArg<bool>();

    cmdMessenger.readBinArg<bool>();
    cmdMessenger.readBinArg<uint16_t>();
    cmdMessenger.readBinArg<bool>();

    cmdMessenger.readBinArg<unsigned long>();

    cmdMessenger.sendCmd(kError, "Busy");
    // cmdMessenger.sendCmdBinArg<unsigned long>(currentStep.time);
  }
  else
  {
    // String targetPump = cmdMessenger.readBinArg<String>();
    currentStep.stateA = cmdMessenger.readBinArg<bool>();
    currentStep.speedA = cmdMessenger.readBinArg<uint16_t>();
    currentStep.dirA = cmdMessenger.readBinArg<bool>();

    currentStep.stateB = cmdMessenger.readBinArg<bool>();
    currentStep.speedB = cmdMessenger.readBinArg<uint16_t>();
    currentStep.dirB = cmdMessenger.readBinArg<bool>();

    currentStep.stateC = cmdMessenger.readBinArg<bool>();
    currentStep.speedC = cmdMessenger.readBinArg<uint16_t>();
    currentStep.dirC = cmdMessenger.readBinArg<bool>();

    if (currentStep.stateA)
    {
      StartPumpA(currentStep.speedA, currentStep.dirA);
    }
    else
    {
      StopPumpA();
    }
    if (currentStep.stateB)
    {

      StartPumpB(currentStep.speedB, currentStep.dirB);
    }
    else
    {
      StopPumpB();
    }
    if (currentStep.stateC)
    {

      StartPumpC(currentStep.speedC, currentStep.dirC);
    }
    else
    {
      StopPumpC();
    }

    pumpA.state = currentStep.stateA;
    pumpA.speed = currentStep.speedA;
    pumpA.dir = currentStep.dirA;

    pumpB.state = currentStep.stateB;
    pumpB.speed = currentStep.speedB;
    pumpB.dir = currentStep.dirB;

    pumpC.state = currentStep.stateC;
    pumpC.speed = currentStep.speedC;
    pumpC.dir = currentStep.dirC;

    currentStep.time = cmdMessenger.readBinArg<unsigned long>();

    currentStep.state = true;
    currentStep.done = false;
    currentStep.stepStartTime = millis();

    cmdMessenger.sendCmdStart(kAcknowledge);
    cmdMessenger.sendCmdArg("Step");
    // cmdMessenger.sendCmdBinArg<unsigned long>(currentStep.time);
    cmdMessenger.sendCmdEnd();
  }
}

void receiveStop()
{

  stopPumps();

  currentStep.done = true;
  currentStep.state = false;
  cmdMessenger.sendCmd(kAcknowledge, "Stopped");
}
