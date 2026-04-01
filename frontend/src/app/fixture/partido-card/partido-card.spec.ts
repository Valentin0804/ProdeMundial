import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PartidoCard } from './partido-card';

describe('PartidoCard', () => {
  let component: PartidoCard;
  let fixture: ComponentFixture<PartidoCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PartidoCard],
    }).compileComponents();

    fixture = TestBed.createComponent(PartidoCard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
