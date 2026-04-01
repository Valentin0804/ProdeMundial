import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FixtureGrupos } from './fixture-grupos';

describe('FixtureGrupos', () => {
  let component: FixtureGrupos;
  let fixture: ComponentFixture<FixtureGrupos>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FixtureGrupos],
    }).compileComponents();

    fixture = TestBed.createComponent(FixtureGrupos);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
