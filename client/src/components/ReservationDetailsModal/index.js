import React, { Component } from 'react';
import settings from '../../config/settings';
import './ReservationDetailsModal.scss';
import { Button, Header, Modal } from 'semantic-ui-react'

class ReservationDetailsModal extends Component {
  componentDidMount() {
    console.log(settings)
  }

  render() {
    return (
      <div id="reservation-details-modal">
        <Modal trigger={<Button>Show Modal</Button>} centered={false}>
          <Modal.Header>Reservation Details</Modal.Header>
          <Modal.Content image>
            <Modal.Description>
              <Header>Room #</Header>
              <p>Date: </p>
              <p>From:</p>
              <p>We've found the following gravatar image associated with your e-mail address.</p>
              <p>Is it okay to use this photo?</p>
            </Modal.Description>
          </Modal.Content>
        </Modal>
      </div>
    )
  }
}

export default ReservationDetailsModal;
