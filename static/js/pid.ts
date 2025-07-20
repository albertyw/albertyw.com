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

/*
function roundToTwoDecimalPlaces(value: number): string {
  let output = value.toFixed(2);
  output = ' '.repeat(6 - output.length) + output;
  return output;
}
*/

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

function runPID(pid: PID): Data {
  const pidController = createPIDController(pid);

  const data: Data = {
    setPoints: [],
    measuredValues: [],
    outputs: []
  };

  const stepCount = 100;
  const setPoint = 10;
  let measuredValue = 5;
  // console.log('  Step', 'Set Point', 'Measured Value', 'PID Output');
  for (let step = 0; step < stepCount; step++) {
    const output = pidController(setPoint, measuredValue);

    data.setPoints.push(setPoint);
    data.measuredValues.push(measuredValue);
    data.outputs.push(output);

    // Output
    /*
    const row = [
      roundToTwoDecimalPlaces(step),
      roundToTwoDecimalPlaces(setPoint),
      roundToTwoDecimalPlaces(measuredValue),
      roundToTwoDecimalPlaces(output)
    ];
    console.log(...row);
    */

    // Simulate system response
    measuredValue = measuredValue + output * 0.1;
  }
  return data;
}

export function main(): void {
  if (document.getElementById('pidChart') === null) {
    return;
  }
  const datasets = [];
  for (const p of [0.1, 1.0, 5.0]) {
    for (const i of [0.0, 0.1]) {
      for (const d of [0.0, 1.0]) {
        const pid: PID = { kp: p, ki: i, kd: d };
        const result = runPID(pid);
        if (datasets.length === 0) {
          datasets.push({
            label: 'Set Points',
            data: result.setPoints,
          });
        }
        const label = `P: ${p.toFixed(1)}, I: ${i.toFixed(1)}, D: ${d.toFixed(2)}`;
        datasets.push({
          label: label,
          data: result.measuredValues,
          borderColor: `hsl(${Math.random() * 360}, 100%, 50%)`,
          fill: false
        });
      }
    }
  }
  new Chart(
    document.getElementById('pidChart') as HTMLCanvasElement,
    {
      type: 'line',
      data: {
        labels: datasets[0].data.map((_, index) => index),
        datasets: datasets,
      }
    }
  );
}
