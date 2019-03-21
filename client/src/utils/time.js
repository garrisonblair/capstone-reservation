function generateMinuteOptions(minuteInterval) {
  const result = [];
  for (let i = 0; i < 60; i += minuteInterval) {
    result.push({
      text: `${i < 10 ? `0${i}` : i}`,
      value: `${i < 10 ? `0${i}` : i}`,
    });
  }
  return result;
}

function generateHourOptions(minHour, maxHour) {
  const result = [];
  for (let i = minHour; i < maxHour; i += 1) {
    result.push({
      text: `${i}`,
      value: `${i}`,
    });
  }
  return result;
}

const timeUtil = {
  generateMinuteOptions,
  generateHourOptions,
};

export default timeUtil;
