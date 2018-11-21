import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Form, Input, Button, Icon, Step, Loader } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
import './Registration.scss';


class Registration extends Component {

  state = {
    encsUsername: '',
    modalType: 'info',
    showLoader: false,
  };

  componentWillMount() {
    const { showLoaderForTest } = this.props;
    // This is only for testing.
    if (showLoaderForTest) {
      this.setState({ showLoader: true });
    }
  }

  handleEncsUsername = (event) => {
    this.setState({ encsUsername: event.target.value });
  }

  closeModal = () => {
    const { modalType } = this.state;
    const { history } = this.props;
    if (modalType === 'success') {
      history.push('/');
    }
  }

  sendEmail = () => {
    const { encsUsername } = this.state;

    this.setState({ showLoader: true });

    api.register(encsUsername)
      .then((response) => {
        if (response.status === 201) {
          this.setState({
            showLoader: false,
          });
          sweetAlert(
            'A verification link has been sent to your ENCS email account.',
            'Please click on the link to continue the registration process.',
            'success',
          );
        }
      })
      .catch((error) => {
        this.setState({ showLoader: false });
        if (error.message.includes('302')) {
          sweetAlert(
            'You are already registered',
            'A verification email has already been sent to your ENCS email. Please double check.',
            'warning',
          );
        } else if (error.message.includes('400')) {
          sweetAlert(
            'Error',
            "We couldn't find this user in the system.",
            'error',
          );
        }
      });
  }

  renderLoader() {
    return (
      <div>
        <Loader active inline="centered" size="large" />
      </div>
    );
  }

  renderMainForm() {
    return (
      <div>
        <h1>Registration</h1>
        <Step.Group size="mini" widths={2}>
          <Step active>
            <Icon name="envelope" />
            <Step.Content>
              <Step.Title>Step 1</Step.Title>
              <Step.Description>ENCS username verification</Step.Description>
            </Step.Content>
          </Step>
          <Step>
            <Icon name="cog" />
            <Step.Content>
              <Step.Title>Step 2</Step.Title>
              <Step.Description>Account setup</Step.Description>
            </Step.Content>
          </Step>
        </Step.Group>
        <p>Please enter your ENCS username. A validation will be sent to your ENCS email.</p>
        <Form.Field>
          <Input
            fluid
            size="small"
            icon="user"
            iconPosition="left"
            placeholder="ex. a_test"
            onChange={this.handleEncsUsername}
          />
        </Form.Field>
        <Form.Field>
          <br />
          <Button fluid size="small" icon onClick={this.sendEmail}>
            Send Email
          </Button>
        </Form.Field>
      </div>
    );
  }

  render() {
    const { showLoader } = this.state;
    return (
      <div id="registration">
        <div className="container">
          {showLoader ? this.renderLoader() : this.renderMainForm()}
        </div>
      </div>
    );
  }
}

Registration.propTypes = {
  showLoaderForTest: PropTypes.bool,
};

Registration.defaultProps = {
  showLoaderForTest: false,
};

export default Registration;
