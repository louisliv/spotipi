import React, { useEffect, useState } from "react";

import { Form } from "react-bootstrap";

const Settings = () => {
  const [settings, setSettings] = useState<any>({});

  useEffect(() => {
    fetch("/api/settings/")
      .then((res) => res.json())
      .then((data) => {
        setSettings(data);
      });
  }, []);

  const updateSettings = async (event: any) => {
    const target = event.target;
    const value = target.checked;
    const name = target.name;
    const current = settings;

    try {
      const response = await fetch("/api/settings/", {
        method: "POST",
        body: JSON.stringify({
          [name]: value,
        }),
      })
      
      if (response.status >= 400) throw new Error(await response.json());

      const data = await response.json();

      setSettings(data);
    } catch (error) {
      setSettings(current);
    }
  }

  return (
    <div>
      <h1 className="mt-3">Settings</h1>
      <Form>
        <Form.Group className="mb-3" controlId="formShuffle">
          <Form.Label>Shuffle on play</Form.Label>
          <Form.Check 
            name="shuffle"
            type="switch"
            checked={settings.shuffle}
            onChange={updateSettings}
            />
        </Form.Group>
      </Form>
    </div>
  );
}

export default Settings;
