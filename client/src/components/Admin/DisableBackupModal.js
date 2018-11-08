import React, {Component} from 'react';
import {Button, Form, Modal, Header} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';


class DisableBackupModal extends Component {

  disableBackup = (e) => {
    let data = {
      is_webcalendar_backup_active: false,
    }

    api.updateAdminSettings(data)
    .then((response) => {
      sweetAlert(
        'Completed',
        'Settings were successfully saved.',
        'success'
      )
      this.props.onClose();
    })
    .catch((error) => {
      console.log(error);
    })
  }

  render() {
    return (
      <Modal open={this.props.show}>
        <Header>
          <h1 className="login__container__header__title">
            {'Disable automatic backup?'}
          </h1>
        </Header>
        <div className="login__container__main">
          <div className="ui divider"/>
          <div className="login__container__main__form-wrapper">
            <Form.Field>
              <Button fluid size='small' icon onClick={this.disableBackup}>
                Confirm
              </Button>
            </Form.Field>
            <div className="ui divider"/>
          </div>
        </div>
      </Modal>
    )
  }
}

export default DisableBackupModal;
