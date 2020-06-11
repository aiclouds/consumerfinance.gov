/**
 * Update the application state model, then trigger updates in views
 */
import { navigationView } from '../views/navigation-view.js';
import { stateModel } from '../models/state-model.js';
import { updateCostOfBorrowingChart, updateMakePlanChart, updateMaxDebtChart } from '../dispatchers/update-view.js';

const updateState = {

  /**
   * activeSection - Change the active navigation view, trigger an update
   * for the navigationView
   *
   * @param {string} item - Value of 'data-nav_item' attribute
   */
  activeSection: item => {
    stateModel.setValue( 'activeSection', item );
    if ( item === 'make-a-plan' ) {
      updateMakePlanChart();
    } else if ( item === 'max-debt-guideline' ) {
      updateMaxDebtChart();
    } else if ( item === 'cost-of-borrowing' ) {
      updateCostOfBorrowingChart();
    }
  },

  getStarted: bool => {
    if ( bool === true ) {
      stateModel.setValue( 'gotStarted', true );
    }
  },

  nextSection: () => {
    const i = stateModel.sectionOrder.indexOf( stateModel.values.activeSection );
    if ( i !== -1 ) {
      const nextSection = stateModel.sectionOrder[i + 1];
      updateState.activeSection( nextSection );
    }
  },

  byProperty: function( prop, value ) {
    stateModel.setValue( prop, value );
  }

};

export {
  updateState
};
