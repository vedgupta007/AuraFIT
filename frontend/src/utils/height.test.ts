import { describe, it, expect } from 'vitest';
import { cmToFtIn, ftInToCm } from './height';

describe('Height Conversion Utilities', () => {
  it('converts valid feet and inches to cm accurately', () => {
    expect(ftInToCm(5, 8)).toBe(173);
    expect(ftInToCm(6, 0)).toBe(183);
    expect(ftInToCm(5, 11)).toBe(180);
    expect(ftInToCm(0, 5)).toBe(13);
  });

  it('rejects inches greater than 11', () => {
    expect(() => ftInToCm(5, 12)).toThrow('Invalid feet or inches');
    expect(() => ftInToCm(5, 15)).toThrow('Invalid feet or inches');
  });

  it('rejects negative values', () => {
    expect(() => ftInToCm(-1, 5)).toThrow('Invalid feet or inches');
    expect(() => ftInToCm(5, -1)).toThrow('Invalid feet or inches');
  });

  it('converts cm to feet and inches accurately', () => {
    expect(cmToFtIn(173)).toEqual({ ft: 5, in: 8 });
    expect(cmToFtIn(183)).toEqual({ ft: 6, in: 0 });
    expect(cmToFtIn(180)).toEqual({ ft: 5, in: 11 });
  });

  it('handles edge case where cm rounds up to exactly 12 inches', () => {
    // 182.88 cm is exactly 6'0"
    expect(cmToFtIn(182.88)).toEqual({ ft: 6, in: 0 });
  });
});
