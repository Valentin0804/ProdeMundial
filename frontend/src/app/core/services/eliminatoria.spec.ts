import { TestBed } from '@angular/core/testing';

import { Eliminatoria } from './eliminatoria';

describe('Eliminatoria', () => {
  let service: Eliminatoria;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Eliminatoria);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
