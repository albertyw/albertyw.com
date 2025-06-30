import Chart from 'chart.js/auto';

type PID = {
  kp: number; // Proportional gain
  ki: number; // Integral gain
  kd: number; // Derivative gain
};

type DataSeries = number[];

type Data = {
  setPoints: DataSeries;       // Desired values to achieve
  measuredValues: DataSeries;  // Actual values measured
  outputs: DataSeries;         // Control outputs computed by the PID controller
};

function roundToTwoDecimalPlaces(value: number): string {
  let output = value.toFixed(2);
  output = ' '.repeat(6 - output.length) + output;
  return output;
}

function createPIDController(pid: PID): (setPoint: number, measuredValue: number) => number {
  let integral = 0;
  let previousError = 0;

  return (setPoint: number, measuredValue: number): number => {
    const error = setPoint - measuredValue;
    integral += error;
    const derivative = error - previousError;

    const output = pid.kp * error + pid.ki * integral + pid.kd * derivative;

    previousError = error;

    return output;
  };
}

function runPID(): void {
  const pid: PID = { kp: 1.0, ki: 0.1, kd: 0.01 };
  const pidController = createPIDController(pid);

  const data: Data = {
    setPoints: [],
    measuredValues: [],
    outputs: []
  };

  const stepCount = 20;
  const setPoint = 10;
  let measuredValue = 8;
  console.log('  Step', 'Set Point', 'Measured Value', 'PID Output');
  for (let step = 0; step < stepCount; step++) {
    const output = pidController(setPoint, measuredValue);

    data.setPoints.push(setPoint);
    data.measuredValues.push(measuredValue);
    data.outputs.push(output);

    // Output
    const row = [
      roundToTwoDecimalPlaces(step),
      roundToTwoDecimalPlaces(setPoint),
      roundToTwoDecimalPlaces(measuredValue),
      roundToTwoDecimalPlaces(output)
    ];
    console.log(...row);

    // Simulate system response
    measuredValue = measuredValue + output * 0.1;
  }
}

export function main(): void {
  runPID();
  const data = [
    { year: 2010, count: 10 },
    { year: 2011, count: 20 },
    { year: 2012, count: 15 },
    { year: 2013, count: 25 },
    { year: 2014, count: 22 },
    { year: 2015, count: 30 },
    { year: 2016, count: 28 },
  ];
  new Chart(
    document.getElementById('pidChart') as HTMLCanvasElement,
    {
      type: 'bar',
      data: {
        labels: data.map(row => row.year),
        datasets: [
          {
            label: 'Acquisitions by year',
            data: data.map(row => row.count)
          }
        ]
      }
    }
  );
}
