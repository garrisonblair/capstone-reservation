import React, { Component } from 'react';
import api from '../../utils/api';


function AdminRequired(InnerComponent) {
  class HOC extends Component {
    componentDidMount() {
      const { history } = this.props;

      if (!localStorage.CapstoneReservationUser) {
        history.push('/404');
        return;
      }

      api.getMyUser()
        .then((response) => {
          const { data } = response;
          if (!data.is_superuser) {
            history.push('/404');
          }
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.log(error);
        });
    }

    render() {
      return <InnerComponent {...this.props} />;
    }
  }

  return HOC;
}

export default AdminRequired;
