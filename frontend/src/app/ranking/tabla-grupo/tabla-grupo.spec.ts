import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TablaGrupo } from './tabla-grupo';

describe('TablaGrupo', () => {
  let component: TablaGrupo;
  let fixture: ComponentFixture<TablaGrupo>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TablaGrupo],
    }).compileComponents();

    fixture = TestBed.createComponent(TablaGrupo);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
