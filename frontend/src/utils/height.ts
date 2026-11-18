export function cmToFtIn(cm: number): { ft: number; in: number } {
  const totalInches = cm / 2.54;
  const ft = Math.floor(totalInches / 12);
  const inches = Math.round(totalInches % 12);
  
  if (inches === 12) {
    return { ft: ft + 1, in: 0 };
  }
  return { ft, in: inches };
}

export function ftInToCm(ft: number, inches: number): number {
  if (ft < 0 || inches < 0 || inches > 11) {
    throw new Error('Invalid feet or inches');
  }
  return Math.round((ft * 12 + inches) * 2.54);
}
