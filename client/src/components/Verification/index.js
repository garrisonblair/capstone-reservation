import axios from 'axios';
import settings from '../../config/settings';
import React, {Component} from 'react';
import './Verification.scss';


class Verification extends Component {

  componentWillMount() {
    const {token} = this.props.match.params;
    console.log(token);
    if (token) {
      const data = {"token": `${token}`}
      axios({
        method: 'POST',
        url: `${settings.API_ROOT}/verify`,
        data: data
      })
        .then((response) => {
          this.setState({
            isVerified: true
          });
          console.log('verification succeed');
        })
        .catch((error) => {
          console.log('verification failed')
        })
    }
  }

  render() {
    return (
      <div id="verification">
        <h1> Verification </h1>
      </div>
    )
  }
}

export default Verification;
