const days = [
  "monday",
  "tuesday",
  "wendesday",
  "thursday",
  "friday",
  "saturday",
  "sunday",
];

function prep_data_from_one_device(device, day) {
  let data = Array(25)
    .fill()
    .map(() => 0);
  device.timestamps
    .filter((i) => i.weekdays[day] == true)
    .forEach((n) => {
      for (let i = n.start; i < n.end; ++i) data[i] = device.parameter;
    });
  return data;
}

function prep_data_from_week(device) {
  return [].concat(...days.map((i) => prep_data_from_one_device(device, i)));
}

function x_data() {
  return [].concat(
    ...days.map((day) => [...hours].map((hour) => `${hour}:00 - ${day}`))
  );
}

function prep_power_usage_traces(devices) {
  const x = x_data();
  return devices
    .filter((dev) => dev.device_type == 0)
    .map((dev) => ({
      x: x,
      y: prep_data_from_week(dev),
      type: "scatter",
      mode: "lines",
      name: dev.name,
    }));
}

function sum_devices_for_day(devices, day) {
  const arrays = devices.map((elem) => prep_data_from_one_device(elem, day));
  let result = hours.map(() => 0);
  for (let j = 0; j < hours.length; ++j) {
    for (let i = 0; i < arrays.length; ++i) {
      result[j] -= arrays[i][j];
    }
  }
  return result;
}

function prep_solar_eff(devices) {
  const defs = devices.filter((dev) => dev.device_type == 0);
  const solars = devices.filter((dev) => dev.device_type == 1);
  const accs = devices.filter((dev) => dev.device_type == 2);
  const limit = accs.reduce((acc, n) => acc + n.parameter, 0);
  let accumulator = [];
  let defs_acc = [];
  let to_pay_acc = [];
  for (const day of days) {
    let usage = sum_devices_for_day(defs, day);
    defs_acc = defs_acc.concat(usage);
    let payment = [...usage];
    for (const solar of solars) {
      for (const timestamp of solar.timestamps) {
        if (timestamp.weekdays[day] == true) {
          for (let i = timestamp.start; i < timestamp.end; ++i) {
            usage[i] += solar.parameter;
            payment[i] += solar.parameter;
            if (usage[i] > limit) usage[i] = limit;
          }
        }
      }
      accumulator.push(usage);
    }
    to_pay_acc.push(payment);
  }
  console.log(to_pay_acc);
  const x = x_data();
  return [
    {
      x: x,
      y: [].concat(...accumulator).map((elem) => (elem < 0 ? 0 : elem)),
      type: "scatter",
      mode: "lines",
      name: "generated power",
    },
    {
      x: x,
      y: defs_acc,
      type: "scatter",
      mode: "lines",
      name: "used power",
    },
    {
      x: x,
      y: defs_acc.map(() => limit),
      type: "scatter",
      mode: "lines",
      name: "capacity",
    },
    {
      x: x,
      y: []
        .concat(...to_pay_acc)
        .map((e) => -e)
        .map((e) => (e > 0 ? e : 0)),
      type: "scatter",
      mode: "lines",
      name: "payment",
    },
  ];
}
