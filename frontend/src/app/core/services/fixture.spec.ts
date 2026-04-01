import { TestBed } from '@angular/core/testing';

import { Fixture } from './fixture';

describe('Fixture', () => {
  let service: Fixture;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Fixture);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
