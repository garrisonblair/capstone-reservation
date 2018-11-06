import React, {Component} from 'react';
import { Modal, Button } from 'semantic-ui-react';


class RoomModal extends Component {
  render() {
    let  {show} = this.props;
    return(
      <div id="room-modal">
        <Modal centered={false} size={"tiny"} open={show}>
        <Modal.Header>
            {/* <Icon name="map marker alternate" /> */}
            Room Details
          </Modal.Header>
          <Modal.Content>
          <Modal.Description>
            <Button onClick={this.props.closeModal}>Close</Button>
          </Modal.Description>
          </Modal.Content>
        </Modal>
      </div>
    )

  }
}

export default RoomModal;
