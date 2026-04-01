import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LlaveCard } from './llave-card';

describe('LlaveCard', () => {
  let component: LlaveCard;
  let fixture: ComponentFixture<LlaveCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LlaveCard],
    }).compileComponents();

    fixture = TestBed.createComponent(LlaveCard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
