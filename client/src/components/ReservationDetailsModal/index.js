import React, {Component} from 'react';
import settings from '../../config/settings';
import './ReservationDetailsModal.scss';


class ReservationDetailsModal extends Component {
  componentDidMount() {
    console.log(settings)
  }

  render() {
    return (
      <div id="reservation-details-modal">
        <h1> ReservationDetailsModal </h1>
      </div>
    )
  }
}

export default ReservationDetailsModal;
