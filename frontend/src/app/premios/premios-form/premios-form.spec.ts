import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PremiosForm } from './premios-form';

describe('PremiosForm', () => {
  let component: PremiosForm;
  let fixture: ComponentFixture<PremiosForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PremiosForm],
    }).compileComponents();

    fixture = TestBed.createComponent(PremiosForm);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
