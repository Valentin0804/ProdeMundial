import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GrupoCard } from './grupo-card';

describe('GrupoCard', () => {
  let component: GrupoCard;
  let fixture: ComponentFixture<GrupoCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GrupoCard],
    }).compileComponents();

    fixture = TestBed.createComponent(GrupoCard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
