using UnityEngine;
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Collections.Concurrent;
using System.Collections.Generic;

public class Receiver : MonoBehaviour
{
    [Header("UDP")]
    [SerializeField] private int rxPort = 8000;

    [Header("Piano")]
    [SerializeField] private Transform pianoRoot;
    [SerializeField] private KeyMotionThemeManager themeManager;

    private UdpClient client;
    private Thread receiveThread;
    private volatile bool isRunning;

    private readonly ConcurrentQueue<string> receivedMessages =
        new ConcurrentQueue<string>();

    private readonly Dictionary<string, Key_Animation> pianoKeys =
        new Dictionary<string, Key_Animation>();


    private void Start()
    {
        RegisterPianoKeys();
        StartReceiver();
    }


    private void RegisterPianoKeys()
    {
        if (pianoRoot == null)
        {
            Debug.LogError(
                "Piano Root n’est pas assigné dans UdpSocket."
            );

            return;
        }

        Key_Animation[] keys =
            pianoRoot.GetComponentsInChildren<Key_Animation>(true);

        foreach (Key_Animation key in keys)
        {
            string note = key.NoteName;

            if (string.IsNullOrWhiteSpace(note))
            {
                Debug.LogWarning(
                    "Une touche PianoKey n’a pas de Note Name.",
                    key
                );

                continue;
            }

            if (pianoKeys.ContainsKey(note))
            {
                Debug.LogWarning(
                    $"La note {note} est présente plusieurs fois."
                );

                continue;
            }

            pianoKeys.Add(note, key);
        }

        Debug.Log(
            $"{pianoKeys.Count} touches enregistrées dans KeyMotion."
        );
    }


    private void StartReceiver()
    {
        try
        {
            client = new UdpClient(rxPort);
            isRunning = true;

            receiveThread = new Thread(ReceiveData);
            receiveThread.IsBackground = true;
            receiveThread.Start();

            Debug.Log(
                $"UDP receiver started on port {rxPort}"
            );
        }
        catch (Exception error)
        {
            Debug.LogError(
                "UDP initialization error: " + error.Message
            );
        }
    }


    private void ReceiveData()
    {
        IPEndPoint sender =
            new IPEndPoint(IPAddress.Any, 0);

        while (isRunning)
        {
            try
            {
                byte[] data = client.Receive(ref sender);

                string message =
                    Encoding.UTF8.GetString(data);

                receivedMessages.Enqueue(message);
            }
            catch (ObjectDisposedException)
            {
                break;
            }
            catch (SocketException error)
            {
                if (isRunning)
                {
                    Debug.LogWarning(
                        "UDP socket error: " + error.Message
                    );
                }
            }
            catch (Exception error)
            {
                if (isRunning)
                {
                    Debug.LogError(
                        "UDP receive error: " + error.Message
                    );
                }
            }
        }
    }


    private void Update()
    {
        while (receivedMessages.TryDequeue(out string message))
        {
            ProcessInput(message);
        }
    }


    private void ProcessInput(string input)
{
    if (string.IsNullOrWhiteSpace(input))
        return;

    string[] messageParts =
        input.Trim()
             .ToUpperInvariant()
             .Split('|');

    if (messageParts.Length != 2)
    {
        Debug.LogWarning(
            "Message UDP invalide : " + input
        );

        return;
    }

    string note = messageParts[0];
    string action = messageParts[1];

    if (note == "COLOR" && action == "NEXT")
    {
        if (themeManager == null)
        {
            Debug.LogWarning("ThemeManager non assigné dans Receiver.");
            return;
        }

        themeManager.NextTheme();
        return;
    }

    if (!pianoKeys.TryGetValue(
        note,
        out Key_Animation key
    ))
    {
        Debug.LogWarning(
            "Touche Unity introuvable : " + note
        );

        return;
    }

    if (action == "PRESS")
    {
        key.SetPressed(true);
    }
    else if (action == "RELEASE")
    {
        key.SetPressed(false);
    }
    else
    {
        Debug.LogWarning(
            "Action inconnue : " + action
        );
    }

    // Debug.Log(
    //     $"Message reçu : {note} | {action}"
    // );
}


    private void OnDisable()
    {
        StopReceiver();
    }


    private void OnApplicationQuit()
    {
        StopReceiver();
    }


    private void StopReceiver()
    {
        if (!isRunning)
        {
            return;
        }

        isRunning = false;

        if (client != null)
        {
            client.Close();
            client = null;
        }

        if (receiveThread != null &&
            receiveThread.IsAlive)
        {
            receiveThread.Join(500);
        }

        receiveThread = null;

        Debug.Log("UDP receiver stopped");
    }
}